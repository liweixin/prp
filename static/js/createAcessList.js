function autocreate(){
	//����table���
	var table=document.createElement("table");
	table.setAttribute("border","3");
	//��ȡ����ֵ
	var list=document.getElementById("list").value;
	var apAcessRecord=document.getElementById("apAcessRecord").value;
	var json = JSON.parse(apAcessRecord);
	var line = json.length;
	//����б�����
	var tr=document.createElement("tr");
	for(obj in json[0]){
		//alert(list);
		//����td
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
		//����tr
		var tr=document.createElement("tr");
		for(obj in json[i]){
			//alert(list);
			//����td
			var td=document.createElement("td");
			td.innerHTML=json[i][obj];
			tr.appendChild(td);
		}
		var td=document.createElement("td");
		td.innerHTML='<a href="/apacessrecord" onclick=""> Edit</a>';
		tr.appendChild(td);
		var td=document.createElement("td");
		td.innerHTML='<a href=/acessInfos/del/' + json[i]['startTime'] + ' onclick=""> Delete</a>';
		tr.appendChild(td);
		table.appendChild(tr); 
	}
	document.getElementById("d1").appendChild(table);
}

autocreate();