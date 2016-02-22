// 百度地图API功能
var map = new BMap.Map("allmap", {enableMapClick:false});     //构造底图时，关闭底图可点功能
var point = new BMap.Point(116.404, 39.915);
map.centerAndZoom(point, 18);
map.enableScrollWheelZoom();                 //启用滚轮放大缩小

//添加覆盖物
function add_overlay(){
	var str = document.getElementById("location").value;
	var json = JSON.parse(str);
	var len = getJsonObjLength(json)
	var myIcon = new BMap.Icon(https://raw.githubusercontent.com/liweixin/prp/master/pic/wifi.png", new BMap.Size(24,24));
	for(var i=0; i<len; i++){
		marker = new BMap.Marker(new BMap.Point(json[i].longtitude, json[i].latitude), {icon:myIcon});
		map.addOverlay(marker);
		add_menu(marker);
	}
	set_zoom(json[0]);
}
//清除覆盖物
function remove_overlay(){
	map.clearOverlays();         
}
function set_zoom(loc){
	var point = new BMap.Point(loc.longtitude, loc.latitude);
	setTimeout(function(){
		map.panTo(point);   //0ms后移动地图
	}, 0);
}
function add_menu(marker){

	//创建右键菜单
	var removeMarker = function(e,ee,marker){
	    map.removeOverlay(marker);
    }
	var showInfo = function(e, ee, marker){
		alert("Wifi information.");
	}
	var markerMenu=new BMap.ContextMenu();
	markerMenu.addItem(new BMap.MenuItem('删除',removeMarker.bind(marker)));
	markerMenu.addItem(new BMap.MenuItem('查看详情',showInfo.bind(marker)));
	marker.addContextMenu(markerMenu);
}
function getJsonObjLength(jsonObj) {
        var Length = 0;
        for (var item in jsonObj) {
            Length++;
        }
        return Length;
}