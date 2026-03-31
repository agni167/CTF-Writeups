# StegoRSA picoCTF Writeup
first things, first, read the challenge and download all the files locally using 'wget [link] command'. now lets move to the analysis part.
"A message has been encrypted using RSA. The public key is gone… but someone might have been careless with the private key. Can you recover it and decrypt the message?"
this can fairly give the idea that the private key is encoded somewhere in the files itself, and we need to use some tools or intiution to get that, plug the key into the file and get the flag.

as we can look, there is an image.jpg file provided to us.
## Step 1
go to the terminal and type `exiftool image.jpg`

now there is a hell lot of appended text in the comment tag in the image metadata.

## Step 2

this dosent look like random text, so we will just go to cyberchef and figure out there itself.

now when we look at the pasted text in the input section and then click the magic wand button, we get text starting with "----BEGIN PRIVATE KEY-----" and "----END PRIVATE KEY----"

## Step 3
now when we already have the private key, most of our job is done, we just need to plug in the key to `flag.pem` and get the flag.

but first we need to save the key to a file ending with .pem.
run `nano key.pem`
paste the full key along with headers.

## Step 4
now plug in the key file into the target file and get the flag.

`openssl rsautl -decrypt -inkey key.pem -in flag.enc`

thats it, you will now see the flag in your terminal.

`picoCTF{rs4_k3y_1n_1mg_ce170c3d}`