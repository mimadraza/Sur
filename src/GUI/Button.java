package GUI;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.RoundRectangle2D;

public class Button extends JButton
{
    private boolean hovered = false;
    private boolean pressed = false;

    public Button(String text)
    {
        super(text);
        setContentAreaFilled(false);
        setFocusPainted(false);
        setFont(new Font("Arial", Font.BOLD, 16));
        setBorder(BorderFactory.createEmptyBorder(10, 25, 10, 25));
        setForeground(Color.WHITE);

        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                hovered = true;
                repaint();
            }

            @Override
            public void mouseExited(MouseEvent e) {
                hovered = false;
                repaint();
            }

            @Override
            public void mousePressed(MouseEvent e) {
                pressed = true;
                repaint();
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                pressed = false;
                repaint();
            }
        });

    }

    @Override
    protected void paintComponent(Graphics g)
    {
        Graphics2D g2d = (Graphics2D) g.create();

        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        if (pressed) {
            g2d.setPaint(new GradientPaint(0, 0, new Color(102, 0, 255), getWidth(), getHeight(), new Color(76, 0, 153)));
        } else if (hovered) {
            g2d.setPaint(new GradientPaint(0, 0, new Color(153, 51, 255), getWidth(), getHeight(), new Color(102, 0, 255)));
        } else {
            g2d.setPaint(new GradientPaint(0, 0, new Color(102, 0, 255), getWidth(), getHeight(), new Color(153, 51, 255)));
        }
        g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
        g2d.dispose();
        super.paintComponent(g);
    }
}
