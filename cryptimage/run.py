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


#print(logo)

#print("Copyright (c) 2022. All rights reserved. \n\nCASSÉ Victorine \nGADEGBEKU Fabio \nPEREL Thomas \nSTCHEPINSKY Nathan")

#print("""\n
#####################################################
## Anti-spoofing and private photo anti-theft tool ##
#####################################################

#Version beta 1""")

import sys
print(sys.argv)
if len(sys.argv) < 3:
    raise Exception("No enough argument")

cmd = sys.argv[1]
path = sys.argv[2]
password = sys.argv[3]

if cmd== "1":

    #print("\n\n\n ##### SIGNATURE D'IMAGE #####")
    #print("\n[*] Chemin absolu de l'image ")
    #print("\n[*]Attention. Votre mot de passe est l'unique preuve de propriété capable d'en réclamer la légitimité une fois la photo signée. Choisissez le avec soin, et gardez le dans un endroit sûr. CryptImage ne sera pas en mesure de le récupérer.")
    #print("\n[*] Mot de passe")

    from cryptimage.imageToSign import ImageToSign
    from cryptimage.imageToVerify import ImageToVerify
    #print("[*] Signature de l'image ...")
    try :
      ImageToVerify(path, password)
      valid = False
    except :
      valid = True

    if valid:
      image = ImageToSign(path, password)
    else :
      print("FAIL : ")
      print("Cette image est déjà protégé ! Impossible de la signée")
elif cmd=="2":
    #print("\n\n\n ##### VÉRIFICATION DE PROPRIÉTÉ D'IMAGE #####")
    #print("\n[*] Chemin absolu de l'image ")
    #print("\n[*]Attention. Votre mot de passe est l'unique preuve de propriété capable d'en réclamer la légitimité une fois la photo signée. CryptImage ne sera pas en mesure de le récupérer.")
    #print("\n[*] Mot de passe")


    from cryptimage.imageToVerify import ImageToVerify
    #print("[*] Vérification de l'image ...")
    image = ImageToVerify(path, password)


