function FriendReq(name, email, friendship_id) {
    this.name = name;
    this.email = email;
    this.friendship_id = friendship_id;
}
function Location(latitude, longitude){
    this.latitude=latitude;
    this.longitude=longitude;
}

function AddFriend(socket, friendRequestsArray, panelContent) {

    $(currentTab).removeClass('active');
    $(currentTab + ">a").css("color", "white");
    //.css("background-color","#2C3E50");
    $('#addFriend').addClass('active');
    $('#addFriend>a').css("color", "black");
    currentTab = '#addFriend';

    while (panelContent != null && panelContent.firstChild) {
        panelContent.removeChild(panelContent.firstChild);
    }

    var container = $('<div id="container" style="min-height: 55vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');

    var emailInput = $('<input id="emailValue" type="text" placeholder="Email of wanted friend">');

    $(emailInput).addClass("col-xs-12")
        .addClass("form-control")
        .css("margin-bottom", "30px");
    var addButton = $('<button type="button" class="btn btn-success btn-lg">Add friend</button>');


    container.append(emailInput);
    container.append($("<br>"));
    container.append(addButton);
    $(panelContent).append(container);


    addButton.on('click', '', function() {
        var value = $('#emailValue').val();
        socket.emit("friend request", {
            "chat_token": localStorage.CHAT_TOKEN,
            "email": value
        });

        socket.on("bad friend request",function(msg){

            alert(msg);
        });
	


    });
}

function ViewFriendRequests(socket, friendRequestsArray, panelContent) {

    $(currentTab).removeClass('active');
    $(currentTab + ">a").css("color", "white");
    //.css("background-color","#2C3E50");
    $('#friendRequests').addClass('active');
    $('#friendRequests>a').css("color", "black");
    currentTab = '#friendRequests';


    while (panelContent != null && panelContent.firstChild) {
        panelContent.removeChild(panelContent.firstChild);
    }

    for (i = 0; i < friendRequestsArray.length; i++) {
        createFriendRequestManager(socket, friendRequestsArray[i].name, friendRequestsArray[i].email, friendRequestsArray[i].friendship_id);
    }



}

function createFriendRequest(imgSrc, name, friendshipId) {
    var h6 = $("<h4></h4>").text(name);
    var friendreq = $("<a id=fr" + friendshipId + " href='#'' class='list-group-item'></a>");
    friendreq.css("display", "flex")
        .css("flex-direction", "row")
        .css("align-items", "center")
        .css("position", "relative");
    let notificationMessage = $("<span class='glyphicon glyphicon-envelope messageNotification'></span>");

    h6.css("display", "inline-block")
        .css("margin-left", "10px");
    friendreq.append(h6);
    friendreq.append(notificationMessage);

    var containerForButtons = $('<div></div>');

    var acceptButton = $('<button id=btna' + friendshipId + ' type="button" class="btn btn-success">Accept</button>');
    acceptButton.css("margin-right", "20px");

    var declineButton = $('<button id=btnd' + friendshipId + ' type="button" class="btn btn-danger">Decline</button>');

    containerForButtons.append(acceptButton)
        .append(declineButton)
        .css("position", "absolute")
        .css("right", "10px")
        .css("top", "25%");

    friendreq.append(containerForButtons);
    $(panelContent).append(friendreq);
}

function createFriendRequestManager(socket, name, from, friendship_id) {

    createFriendRequest("http://placehold.it/50/FA6F57/fff&text=ME", name, friendship_id);

    $('#btna' + friendship_id).on('click', '', function() {

        var answer = confirm("Are you want to accept the friend request?")
        if (answer) {
            socket.emit("response friend request", {
                "chat_token": localStorage.CHAT_TOKEN,
                "email": from,
                "status": 1
            });

            createFriend(socket, "http://placehold.it/50/FA6F57/fff&text=ME", name, friendship_id);

            $("#fr" + friendship_id).remove();
            //panelContent.removeChild(friendreq);
            //friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
            let posOfNewFriend = friendRequestsArray.map(friend => friend.email).indexOf(from);
            friendRequestsArray.splice(posOfNewFriend, 1);
            friends[friendship_id] = new Friend(name, from);
        }

    });

    $('#btnd' + friendship_id).on('click', '', function() {

        var answer = confirm("Are you want to decline the friend request?")
        if (answer) {
            socket.emit("response friend request", {
                "chat_token": localStorage.CHAT_TOKEN,
                "email": from,
                "status": 0
            });
            $("#fr" + friendship_id).remove();
            //panelContent.removeChild(friendreq);
            let posOfDeletedFriendReq = friendRequestsArray.map(friend => friend.email).indexOf(from);
            friendRequestsArray.splice(posOfDeletedFriendReq, 1);
            //friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
        }

    });

}


  
   

function Widgets(panelContent) {




    $(currentTab).removeClass('active');
    $(currentTab + ">a").css("color", "white");
    //.css("background-color","#2C3E50");
    $('#widgets').addClass('active');
    $('#widgets>a').css("color", "black");
    currentTab = '#widgets';

    while (panelContent != null && panelContent.firstChild) {
        panelContent.removeChild(panelContent.firstChild);
    }


     function getLocation() 
    {
    if (navigator.geolocation)
         navigator.geolocation.getCurrentPosition(showPosition);
    }

    function showPosition(position) 
    {
         lat=position.coords.latitude;
         long=position.coords.longitude;
         
        $.ajax({
	        method: "GET",
	        url: "http://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&APPID=ac3ba0c132415bb20cef3bc050715601",
	        success: function(data)
            {
                 console.log(data);
            }
        });
    }

   
        
    }