package DataStructures;
import Utilities.Song;

public class DoublyLinkedList
{
    private class Node
    {
        private Song data;
        private Node next;
        private Node previous;

        public Node(Song data)
        {
            this.data = data;
            this.next = null;
            this.previous = null;
        }
    }

    private Node head;

    public DoublyLinkedList()
    {
        this.head = null;
    }

    public void add(Song song)
    {
        if(head == null) // initialize head to song if head is null
        {
            head = new Node(song);
            return;
        }

        Node temp = head;

        while(temp.next != null) // for traversing to the last element of the list
        {
            temp = temp.next;
        }

        temp.next = new Node(song); //set the next element to a new song
        temp.next.previous = temp; // set previous to the old last element
    }

    public void remove(Song song)
    {
        if(head.data.equals(song))// if the first element is the song to be removed
        {
            head = head.next;
            head.previous = null;
            return;
        }

        Node temp = head;
        Node previous = head.previous;

        while ( temp !=  null)
        {
            if(temp.data.equals(song))
            {
                previous.next = temp.next;
                temp.next.previous = previous;
                return;
            }

            previous = temp;
            temp = temp.next;
        }
    }

    public int size()
    {
        int size = 0; //initialize counter
        Node temp = head;

        while(temp != null) // loop to traverse
        {
            size++;//increment size
            temp = temp.next;
        }

        return size;
    }
}
