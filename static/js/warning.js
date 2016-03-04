function try_login(logged_in){
	var logged_in=document.getElementById("logged_in").value;
	if(logged_in=="True"){
		alert("You hava logged_in before.");
	} else {
		
	}
	return logged_in=="True";
}
function is_login(logged_in){
	var logged_in=document.getElementById("logged_in").value;
	if(logged_in=="True"){

	} else {
		alert("Please logged_in first.");
	}
}