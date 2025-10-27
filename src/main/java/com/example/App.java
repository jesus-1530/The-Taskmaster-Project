package com.example;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.layout.VBox;
import javafx.scene.control.*;
import javafx.stage.Stage;
import javafx.geometry.Pos;
import javafx.scene.layout.Region;

/*
 user log in page
 */
public class App extends Application {
    @Override
    public void start(Stage stage) {
        stage.setTitle("Log in");

        //project name
        Label nameTitle = new Label("Task Master");
        nameTitle.setStyle("-fx-font-size: 36px; -fx-font-weight: bold;");

        //sign in
        Label title = new Label("Sign In");
        title.setStyle("-fx-font-size: 24px; -fx-font-weight: bold;");

        //account
        TextField username = new TextField();
        username.setPromptText("Username");

        //password
        PasswordField password = new PasswordField();
        password.setPromptText("Password");

        //button
        Button login = new Button("Login");
        login.setMaxWidth(Double.MAX_VALUE); // full width like on a phone


        VBox root = new VBox(15,nameTitle, title, username, password, login);
        root.setAlignment(Pos.CENTER);
        root.setStyle("-fx-padding: 20; -fx-background-color: white;");


        VBox.setMargin(title,new Insets(60,0,0,0));// 60 from nameTitle and title


        Scene scene = new Scene(root, 360, 640); // typical phone resolution
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
