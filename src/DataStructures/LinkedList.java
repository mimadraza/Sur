package DataStructures;

import Utilities.Playlist;

public class LinkedList
{
    private class Node
    {
        private Playlist data;
        private Node next;

        public Node(Playlist data)
        {
            this.data = data;
            this.next = null;
        }
    }

    private Node head;

    public LinkedList()
    {
        this.head = null;
    }

    public void add(Playlist playlist)
    {
        if(head == null)
        {
            head = new Node(playlist);
            return;
        }

        Node temp = head;

        while (temp.next != null)
        {
            temp = temp.next;
        }

        temp.next = new Node(playlist);
    }

    public void remove(Playlist playlist)
    {
        if(head == null)
            return;

        if(head.data.equals(playlist))
        {
            head = head.next;
            return;
        }

        Node temp = head;

        while (temp.next != null)
        {
            if (temp.next.data.equals(playlist)) {
                temp.next = temp.next.next;
                return;
            }

            temp = temp.next;
        }
    }
}
