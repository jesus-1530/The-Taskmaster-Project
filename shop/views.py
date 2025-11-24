from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShopItem, Purchase
from todolist.models import UserProfile


@login_required(login_url='login')
def shop(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST" and "upload_item" in request.POST:
        name = request.POST.get("name")
        description = request.POST.get("description")
        cost = request.POST.get("cost")
        image = request.FILES.get("image")

        if not name or not cost:
            messages.error(request, "Please fill in all required fields.")
        elif int(cost) < 0:
            messages.error(request, "Item cost cannot be negative.")
        elif int(cost) > 999999:
            messages.error(request, "Item cost cannot exceed 999,999 points.")
        else:
            item = ShopItem.objects.create(
                owner=request.user,
                name=name,
                description=description,
                cost=cost,
                image=image
            )
            if image:
                messages.success(request, f"✅ Item added with image: {item.image.url}")
            else:
                messages.success(request, "✅ Item added (no image uploaded)")
        return redirect("shop")

    elif request.method == "POST" and "item_id" in request.POST:
        item_id = request.POST.get("item_id")
        try:
            item = ShopItem.objects.get(id=item_id)
        except ShopItem.DoesNotExist:
            messages.error(request, "Item not found.")
            return redirect("shop")

        if profile.points >= item.cost:
            profile.points -= item.cost
            profile.save()
            Purchase.objects.create(user=request.user, item=item)
            messages.success(request, f"🎉 Purchased {item.name} for {item.cost} points! 🎉")
            item.delete()
        else:
            messages.error(request, f"❌ Insufficient points. You need {item.cost} points but only have {profile.points}. ❌")
            
    items = ShopItem.objects.all()
    return render(request, "shop.html", {
        "profile": profile,
        "items": items,
    })
