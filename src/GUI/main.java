package GUI;

import javax.swing.*;
import java.awt.*;


public class main
{
    public static void main(String[] args)
    {
        JFrame frame = new JFrame();
        frame.setLayout(null);
        frame.setLayout(new BorderLayout());
        frame.setSize((int) Toolkit.getDefaultToolkit().getScreenSize().getWidth(), (int) Toolkit.getDefaultToolkit().getScreenSize().getHeight());
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        LoginPage page = new LoginPage();

        frame.add(page);
        frame.setVisible(true);
    }
}
