function autocreate(){
//����table���
var table=document.createElement("table");
table.setAttribute("border","3");
//��ȡ����ֵ
var line=document.getElementById("line").value;
//��ȡ����ֵ
var list=document.getElementById("list").value;
for(var i=1;i<=line;i++){
//alert(line);
//����tr
var tr=document.createElement("tr");
for(var j=1;j<=list;j++){
//alert(list);
//����td
var td=document.createElement("td");
td.innerHTML=i*j;
tr.appendChild(td);
}
table.appendChild(tr); 
}
document.getElementById("d1").appendChild(table);
}

autocreate();