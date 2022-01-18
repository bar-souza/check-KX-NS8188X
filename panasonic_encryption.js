//--------------------------------------------------------------------------
// Copyright (C) Panasonic R&D Centre Malaysia Sdn. Bhd.
// encrypt.js
// 
// Date	 21/10/2008
// Author	 Teh Hui Chin
//	- Initial version.
//
//---------------------------------------------------------------------------
// CA Server-Requirement Specification-0016 (Teh Hui Chin 21.10.2008)

//---------------------------------------------------------------------
///AlphabetGenerator function description
///
///To generate alphabet 
///
///@param[in] number - number
///
///@return  alphabet - alphabet generated
///              
//----------------------------------------------------------------------
function alphabet_generator(number)
 {
    var input = new Array ("a", "b", "c", "d", "e","f","g","h","i","j","k","l","m","n","o","p","q",
"r","s","t","u","v","w","x","y","z", "a", "b");
    
    return alphabet = input[number];
   
   
 }
 
 
 
 //---------------------------------------------------------------------
///AlphabetGenerator function description
///
///To generate uppercase alphabet 
///
///@param[in] number - number
///
///@return  alphabet - uppercase alphabet generated
///              
//----------------------------------------------------------------------
 function UpperCaseAlphabet_generator(number)
 {
    var input = new Array ("F", "E", "B", "O", "G","O","D","C","H","V","P","I","J","Q","K","R","W",
"N","P","U","M","X","S","Z","T","L", "A", "Y");
    
    return UpperCaseAlphabet = input[number];
   
   
 }
 

// CA Server-System Testing-0069 (Nancy Ang 11.03.2009)
//----------------------------------------------------------------------------------------
/// zeroPad function description
///
/// To pad the string with "0" value so the string length become 3
///
//----------------------------------------------------------------------------------------  
function padWithZero(str, length)
{
	var padString = str.toString(); 
	
	while(padString.length < length)
	{
		padString = "0" + padString; 
	}

	return padString;
}

 
//--------------------------------------------------------------------
///EncryptPassword function description
///
///To generate encrypted password
///
///@param[in] pwdValue - password
///             
//----------------------------------------------------------------------
 function EncryptPassword(pwdValue)
 {  
    var  passwordGenerated ="";
   
    for(var i = 0; i < pwdValue.length; i++)
    {  
       
       var pwd = new Array();
       pwd[i]= pwdValue.charAt(i).charCodeAt()
       /*if(pwd[i]<100)
       {
         if(pwd[i]<=25)
         {
             var k = 25 - pwd[i];
         }
         else if( pwd[i]<=50 && pwd[i]>25)
         {
             var k = 50 - pwd[i];
         }
         else if( pwd[i]<=75 && pwd[i]>50)
         {
             var k = 75 - pwd[i];
         }
         else
         {
             var k = 100 - pwd[i];
         }
         
         pwd[i]=  500 - pwd[i]*2 + alphabet_generator(parseInt(k))+UpperCaseAlphabet_generator(parseInt(k));
       
       }
       else
       {
          var k = 127 - pwd[i];
          pwd[i]= 500 - pwd[i]*2 + UpperCaseAlphabet_generator(parseInt(k)) + alphabet_generator(parseInt(k));
       }
       passwordGenerated += pwd[i];*/
       
       // CA Server-System Testing-0069 (Nancy Ang 11.03.2009)
       var j = pwd[i] % 500;
       var k = pwd[i] / 500;
       var l = pwd[i] % 27;
       
       pwd[i] = padWithZero(500 - j, 3) + "k=" + parseInt(k) + "=k" + UpperCaseAlphabet_generator(parseInt(l)) + alphabet_generator(parseInt(l));

       passwordGenerated += pwd[i];
    }
    
    return passwordGenerated;
 }
 