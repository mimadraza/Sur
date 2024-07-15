package Utilities;

import DataStructures.DoublyLinkedList;


public class Playlist
{
    private String name;
    private DoublyLinkedList list;

    public Playlist(String name)
    {
        this.name = name;
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
