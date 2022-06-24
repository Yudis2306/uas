package com.bigpro.mibird;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class loginactivity extends AppCompatActivity {
    String username="admin";
    String password ="admin";

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        EditText txtUser =findViewById(R.id.textUser);
        EditText txtpass = findViewById(R.id.textPass);
        Button login = findViewById(R.id.btnLogin);

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(txtUser.getText().toString().equalsIgnoreCase(username)&&txtpass.getText().toString().equalsIgnoreCase(password)){
                    startActivity(new Intent(loginactivity.this,HomeActivity.class));

                }else{
                    Toast.makeText(loginactivity.this,"username/password",Toast.LENGTH_SHORT).show();
                }

            }
        });
    }
}
