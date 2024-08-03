package GUI;

import javax.swing.*;
import javax.swing.border.AbstractBorder;
import java.awt.*;
import java.awt.geom.RoundRectangle2D;

public class TextField extends JTextField
{
    private class RoundedBorder extends AbstractBorder {
        private final int radius;
        private final Color borderColor;

        public RoundedBorder(int radius, Color borderColor) {
            this.radius = radius;
            this.borderColor = borderColor;
        }

        @Override
        public void paintBorder(Component c, Graphics g, int x, int y, int width, int height) {
            Graphics2D g2d = (Graphics2D) g.create();
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2d.setColor(borderColor);
            g2d.setStroke(new BasicStroke(2)); // Border width
            g2d.drawRoundRect(0, 0, width - 1, height - 1, radius, radius);
            g2d.dispose();
        }

        @Override
        public Insets getBorderInsets(Component c) {
            return new Insets(5, 5, 5, 5); // Adjust padding as needed
        }
    }

    public TextField(String text) {
        super(text);
        setOpaque(false); // Make background transparent
        setBorder(new RoundedBorder(15, Color.WHITE)); // Set border with rounded corners
        setForeground(Color.WHITE); // Set text color
        setCaretColor(Color.WHITE); // Set cursor color
        setBackground(new Color(0, 0, 0, 0)); // Transparent background
        setFont(new Font("Arial", Font.PLAIN, 16)); // Adjust font as needed
    }
}
