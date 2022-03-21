class CryptImage:
    imageURL: str # Current path of the image to verify
    password: str # Password given by the user

   
    
     

    def __init__(self,imageURL, password):
        if imageURL == "" or imageURL == None or password == "" or password == None :
            raise Exception("Fatal error : User must provide an valide image path and a valid password")
        self.imageURL = imageURL
        self.password = password


    """
        Sign the image which path is imageURL and create the signed image 
        Return the path of the signed image if sucess or a fatal error. 
    """

    def sign(self): 
        pass


    """
       Verify the rights of property related to the given image 
        Return 
            - True if the proof of property is valid
            - False if the proof of property is invalid
            - None if the image isn't signed by Crypt-Image 
    """
    def verify(self):
        pass
