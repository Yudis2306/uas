package com.bigpro.mibird

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.text.Html
import android.view.View
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_result.*


class Aboutactivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about)
        back1.setOnClickListener {
            intent = Intent(this, HomeActivity::class.java)
            startActivity(intent)
        }
        val tvContact = findViewById<View>(R.id.tvContact) as TextView
        tvContact.text = Html.fromHtml("</font><font color='#3b5998'>CONTACT US</font>")
        tvContact.setOnClickListener {
            val email = Intent(Intent.ACTION_SEND)
            email.data = Uri.parse("mailto:")
            email.type = "message/rfc822"
            email.putExtra(Intent.EXTRA_EMAIL, arrayOf("rianpratama6575@gmail.com"))
            startActivity(Intent.createChooser(email, "Send Mail"))
        }
    }
}