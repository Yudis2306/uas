package com.bigpro.mibird;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.net.Uri;


import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

public class HomeActivity extends AppCompatActivity {
    private CardView btn1 ,btn2 ,btn3 ,btn4;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        btn1 =findViewById(R.id.btn1);
        btn2 =findViewById(R.id.btn2);
        btn3 =findViewById(R.id.btn3);
        btn4 =findViewById(R.id.btn4);

        btn1.setOnClickListener(view -> {
//                Toast.makeText(getApplicationContext(),"aloo ini bantun 1",Toast.LENGTH_SHORT).show();
            Intent Intent =new Intent(getApplicationContext(), UploadActivity.class);
            startActivity(Intent);
        });
        btn2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent Intent =new Intent(getApplicationContext(), Aboutactivity.class);
                startActivity(Intent);

            }
        });
        btn3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent Intent =new Intent(getApplicationContext(),loginactivity.class);
                startActivity(Intent);

            }
        });
        btn4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//              String wpurl="https://wa.me/+6285742893181?text=hi,apa kabar ?";
                String wpurl="https://api.whatsapp.com/send/?phone=%2B6285742893181&text=hi%2Capa+kabar&app_absent=0";
                Intent intent=new Intent(Intent.ACTION_VIEW);
                intent.setData(Uri.parse(wpurl));
                startActivity(intent);
            }
        });

    }
}

