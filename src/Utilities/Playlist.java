package Utilities;

import DataStructures.DoublyLinkedList;

import javax.swing.*;
import java.awt.*;


public class Playlist
{
    private String name;
    private Image image;
    private DoublyLinkedList list;

    public Playlist(String name, String path)
    {
        this.name = name;
        this.image = new ImageIcon(path).getImage();
        this.list = null;
    }

    public Playlist(String name, DoublyLinkedList list)
    {
        this.name = name;
        this.list = list;
    }

    public String getName() {
        return name;
    }

    public DoublyLinkedList getList() {
        return list;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setImage(Image image) {
        this.image = image;
    }

    public Image getImage()
    {
        return image;
    }

    @Override
    public boolean equals(Object obj)
    {
        if(!(obj instanceof Playlist))
            return false;

        if(this.name.equals(((Playlist) obj).getName()))
            return true;

        return false;
    }
}
