# PasswprdManager
So first of all you need xampp, and in the PHPAdmin you have to import the sql file.
The code will automatically connect to the databse so you don't have to do anything else.
The code is very simple, just run it and u will know what to do.
In database are 2 tables, one for users and one for passwords from users, any user have an specific id,
after u create an account and login the code will automatically know the user id where will save the data, 
in the second table how i say it saves the data to the specific user id, so when u wanna see the data it will show the data from that id.
The accounts passwords are encrypted with 'from hashlib import sha256' method, but the data is not so the user can see it.
It is not already done, i'm still working on this.
