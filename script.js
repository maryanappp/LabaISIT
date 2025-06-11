$(document).ready(function () {
    let accessToken = "token"; 
    let userId = "id"; 
    let version = "5.131";
    let offset = 0; 
    let friends = [];

    function getFriends() {
        $.ajax({
            url: `https://api.vk.com/method/friends.get`,
            data: {
                user_id: userId,
                access_token: accessToken,
                fields: "city,status,photo_100,last_seen,education,nickname",
                v: version,
                offset: offset,  
            },
            dataType: "jsonp",
            success: function (data) {
                console.log("Ответ от VK API:", data);

                if (data.error) {
                    console.error("Ошибка API:", data.error.error_msg);
                    alert("Ошибка API: " + data.error.error_msg);
                    return;
                }

                friends = friends.concat(data.response.items); 

                
                if (data.response.count > friends.length) {
                    offset = friends.length; 
                    getFriends(); 
                } else {
                    
                    friends.sort((a, b) => (b.last_seen ? b.last_seen.time : 0) - (a.last_seen ? a.last_seen.time : 0));

                    displayFriends(); 
                }
            },
            error: function (jqxhr, textStatus, error) {
                console.error("Ошибка запроса:", textStatus, error);
                alert("Не удалось загрузить список друзей.");
            }
        });
    }

    function displayFriends() {
        $("#friends-list").empty(); 

        
        friends.forEach(friend => showFriend(friend)); 
    }

    function showFriend(friend) {
        let lastSeenDate = friend.last_seen ? new Date(friend.last_seen.time * 1000).toLocaleString() : "Неизвестно";
        let nickname = friend.nickname || "Не указан";
        let education = friend.university_name || "Не указано";

        $("#friends-list").append(
            `<tr>
                <td>${friend.id}</td>
                <td>${friend.first_name}</td>
                <td>${friend.last_name}</td>
                <td>${nickname}</td>
                <td>${education}</td>
                <td>${lastSeenDate}</td>
                <td><img src="${friend.photo_100}" alt="Фото"></td>
            </tr>`
        );
    }

    getFriends(); 
});
