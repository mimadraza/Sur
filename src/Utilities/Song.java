package Utilities;

import java.io.File;

public class Song
{
    private String artistName;
    private String genre;
    private File file;
    private long songLength;

    public Song(String artistName, String genre, File file)
    {
        this.artistName = artistName;
        this.genre = genre;
        this.file = file;
    }

    public long getSongLength()
    {
        return songLength;
    }

    public String getArtistName()
    {
        return artistName;
    }

    public String getGenre()
    {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public void setArtistName(String artistName) {
        this.artistName = artistName;
    }

    public void setFile(File file) {
        this.file = file;
    }

    public void setSongLength(long songLength) {
        this.songLength = songLength;
    }

    public File getFile() {
        return file;
    }

    @Override
    public boolean equals(Object obj)
    {
        if( !(obj instanceof Song))
            return false;
        if( file.getName().equals(((Song) obj).file.getName()))
            return true;

        return false;
    }
}
