package GUI;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class LoginPage extends JPanel implements ActionListener
{
    private Button login;
    private Button signup;
    private TextField userName;
    private PasswordField password;
    private Color backgroundColor = new Color(30, 33, 31);
    private Image poster;

    LoginPage()
    {
        initializeComponents();
    }

    private void initializeComponents()
    {
        this.setLayout(null);
        this.setBackground(backgroundColor);
        this.login = new Button("login");
        this.signup = new Button("sign up");
        this.userName = new TextField("Email");
        this.password = new PasswordField();
        this.poster = new ImageIcon("/home/imad/IdeaProjects/Sur/loginposter.png").getImage();

        userName.setBounds(1200,400,300,60);
        password.setBounds(1200,500,300,60);
        login.setBounds(1300,600,100,50);
        signup.setBounds(1700,850,150,50);
        this.add(userName);
        this.add(password);
        this.add(login);
        this.add(signup);
    }

    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        // Draw the background image
        if (poster != null) {
            g.drawImage(poster, 0, 0, (int) (this.getWidth()*0.4), this.getHeight(), this);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e)
    {

    }
}
