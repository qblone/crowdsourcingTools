
 function validate()
 {
 	var regexp1 = /(https?:\/\/spoofer\.caida\.org)\/report\.php\?sessionkey=([a-zA-Z0-9]{14})/;
    //var regexp1=new RegExp("(https?:\/\/spoofer\.caida\.org)\/report\.php\?sessionkey=([a-zA-Z0-9]{14})");
    
    if(regexp1.test(document.getElementById("id_aform_pre-spoofer_url").value))
        {
           
           
            return true;
        }
    else{

        document.getElementById('error_message').style.display='block';
        
        //document.getElementById('name_error').innerHTML = "<span style='color:#FF0000'>Invalid URL. Please click on the <strong>report</strong> link in application as shown in the figure above.<br\> It will open URL in your browser, please copy and paste the opened URL  in the text box. <br\> Please note that URL will look like http://spoofer.caida.org/report.php?sessionkey= </span>" ;
        return false;




        }
 }



 function validateProA()
 {
    var regexp1 = /(https?:\/\/spoofer\.caida\.org)\/report\.php\?sessionkey=([a-zA-Z0-9]{14})/;
    //var regexp1=new RegExp("(https?:\/\/spoofer\.caida\.org)\/report\.php\?sessionkey=([a-zA-Z0-9]{14})");
    
    if(regexp1.test(document.getElementById("id_proaform-spoofer_url").value))
        {
           
           
            return true;
        }
    else{

        document.getElementById('error_message').style.display='block';
        
        //document.getElementById('name_error').innerHTML = "<span style='color:#FF0000'>Invalid URL. Please click on the <strong>report</strong> link in application as shown in the figure above.<br\> It will open URL in your browser, please copy and paste the opened URL  in the text box. <br\> Please note that URL will look like http://spoofer.caida.org/report.php?sessionkey= </span>" ;
        return false;




        }
 }