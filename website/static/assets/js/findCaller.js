function findCaller() {
// Validation: it must be loaded as the top page, or if it is loaded in an iframe 
// then it must be embedded in my own domain.
// Info: IF top.location.href is not accessible THEN it is embedded in an iframe 
// and the domains are different.
var myresult = true;
try {
    var tophref = top.location.href;
    var tophostname = top.location.hostname.toString();
    document.getElementById('platformname').innerHTML = tophref;
    var myhref = location.href;
    if (tophref === myhref) {
        myresult = true;
    } else if (tophostname !== "www.yourdomain.com") {
        myresult = false;
    }
} catch (error) { 
    var tophref = top.location.href;
    document.getElementById('platformname').innerHTML = tophref;
  // error is a permission error that top.location.href is not accessible 
  // (which means parent domain <> iframe domain)!
    myresult = false;
}
return myresult;
}