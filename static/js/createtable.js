function autocreate(){
	//创建table表格
	var table=document.createElement("table");
	table.setAttribute("border","3");
	//获取列数值
	var list=document.getElementById("list").value;
	var apfeature=document.getElementById("apfeature").value;
	var json = JSON.parse(apfeature);
	var line = json.length;
	//添加列表名称
	var tr=document.createElement("tr");
	for(obj in json[0]){
		//alert(list);
		//创建td
		var td=document.createElement("td");
		td.innerHTML=obj;
		tr.appendChild(td);
	}
	var td=document.createElement("td");
	td.innerHTML='Operation';
	tr.appendChild(td);
	var td=document.createElement("td");
	td.innerHTML='Operation';
	tr.appendChild(td);
	table.appendChild(tr); 
	
	for(var i=0;i<line;i++){
		//alert(line);
		//创建tr
		var tr=document.createElement("tr");
		for(obj in json[i]){
			//alert(list);
			//创建td
			var td=document.createElement("td");
			td.innerHTML=json[i][obj];
			tr.appendChild(td);
		}
		var td=document.createElement("td");
		td.innerHTML='<a href="/apFeatures" onclick=""> Edit</a>';
		tr.appendChild(td);
		var td=document.createElement("td");
		td.innerHTML='<a href=/wifiInfos/del/' + json[i]['bssid'] + ' onclick=""> Delete</a>';
		tr.appendChild(td);
		table.appendChild(tr); 
	}
	document.getElementById("d1").appendChild(table);
}

autocreate();