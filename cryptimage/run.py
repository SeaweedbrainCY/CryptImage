logo = """                                                                                                    

                                       ...................                                          
                                 ..............            ...                                      
                                 ..............             ..                                      
                                 ..............             ...                                     
                               ................              ...                                    
                             ..................                ....                                 
                        .......................                    .....                            
                        .......................                      ...                            
                        .......................                      ...                            
                        .......................                      ..                             
                        .......................                                                     
                         ......................                                                     
                         ......................           ............                              
                          .....................        ...............                              
                           ....................       ......  ......                                
                            ...................      .....      ..         .                        
                             ..................     ......               ...                        
                              .................     .......            .....                        
                                ...............      ........        .......                        
                                  .............       .........    ........                         
                                    ...........        ..................                           
                                      .........           ............                              
                                         ......    ..                                               
                                             ......                                                 
                                                                                                    """


print(logo)

print("Copyright (c) 2022. All rights reserved. \n\nCASSÉ Victorine \nGADEGBEKU Fabio \nPEREL Thomas \nSTCHEPINSKY Nathan")

print("""\n
#####################################################
## Anti-spoofing and private photo anti-theft tool ##
#####################################################

Version beta 1""")

cmd = ""
while cmd != "1" and cmd !="2":
    print("\n\nVoulez vous : \n\n   1. Signer une image\n   2. Réclamer la propriété d'une image")
    print("\n > ", end='')
    cmd = input()

if cmd== "1":

    print("\n\n\n ##### SIGNATURE D'IMAGE #####")
    print("\n[*] Chemin absolu de l'image ")
    path = input(">")
    print("\n[*]Attention. Votre mot de passe est l'unique preuve de propriété capable d'en réclamer la légitimité une fois la photo signée. Choisissez le avec soin, et gardez le dans un endroit sûr. CryptImage ne sera pas en mesure de le récupérer.")
    print("\n[*] Mot de passe")
    password = input(">")


    from cryptimage.imageToSign import ImageToSign
    print("[*] Signature de l'image ...")
    image = ImageToSign(path, password)
elif cmd=="2":
    print("\n\n\n ##### VÉRIFICATION DE PROPRIÉTÉ D'IMAGE #####")
    print("\n[*] Chemin absolu de l'image ")
    path = input(" > ")
    print("\n[*]Attention. Votre mot de passe est l'unique preuve de propriété capable d'en réclamer la légitimité une fois la photo signée. CryptImage ne sera pas en mesure de le récupérer.")
    print("\n[*] Mot de passe")
    password = input(" > ")


    from cryptimage.imageToVerify import ImageToVerify
    print("[*] Vérification de l'image ...")
    image = ImageToVerify(path, password)


