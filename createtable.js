function autocreate(){
//创建table表格
var table=document.createElement("table");
table.setAttribute("border","3");
//获取行数值
var line=document.getElementById("line").value;
//获取列数值
var list=document.getElementById("list").value;
for(var i=1;i<=line;i++){
//alert(line);
//创建tr
var tr=document.createElement("tr");
for(var j=1;j<=list;j++){
//alert(list);
//创建td
var td=document.createElement("td");
td.innerHTML=i*j;
tr.appendChild(td);
}
table.appendChild(tr); 
}
document.getElementById("d1").appendChild(table);
}

autocreate();