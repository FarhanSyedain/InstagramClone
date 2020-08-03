//JS for home page

function include(file) {

    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);

}



//Frontend
var all_like_buttons = document.getElementsByClassName('like_buttons') //All Like Buttons

for (var j = 0; j < all_like_buttons.length; j++) {
    all_like_buttons[j].addEventListener('click', function(e) {
        if (this.classList.contains('non-like')) {
            this.classList.add('like')
            this.classList.remove('non-like')

            id = this.id.split('like')[1]



        } else {
            this.classList.remove('like')
            this.classList.add('non-like')

            id = this.id.split('like')[1] //Will return the id of the post 


        }
    })
}


var all_book_marks = document.getElementsByClassName('book_marks')

for (var i = 0; i < all_book_marks.length; i++) {
    all_book_marks[i].addEventListener('click', function(e) {

        if (this.classList.contains('non-marked')) {
            this.classList.add('marked')
            this.classList.remove('non-marked')

            id = this.id.split('bookmark')[1] //Will return the id of the post 



        } else {
            this.classList.remove('marked')
            this.classList.add('non-marked')

            id = this.id.split('bookmark')[1] //Will return the id of the post 



        }
    })
}

var all_comment_btns = document.getElementsByClassName('comment_button')

for (var i = 0; i < all_comment_btns.length; i++) {
    all_comment_btns[i].addEventListener('click', function(e) {

        id = this.id.split('comment-btn')[1]

        x = 'comment' + id
        var comment_box = document.getElementById(x)


        if (comment_box.classList.contains('hidden')) {

            comment_box.classList.remove('hidden')

        } else {

            comment_box.classList.add('hidden')

        }
    })
}

var all_post_comment_buttons = document.getElementsByClassName('add_comments')
for (var i = 0; i < all_post_comment_buttons.length; i++) {

    all_post_comment_buttons[i].addEventListener('click', function(e) {

        id = this.id.split('addcomment')[1]

        var comment_data = document.getElementById('commentdata' + id)



    })

}


var all_read_mores = document.getElementsByClassName('full_cap')

for (var i = 0; i < all_read_mores.length; i++) {

    all_read_mores[i].addEventListener('click', function(e) {

        id = this.id.split('full')[1]

        document.getElementById('half_caption' + id).classList.add('hidden')
        document.getElementById('full_caption' + id).classList.remove('hidden')

    })

}

//Js for Home ends

//Js for Other pages

var all_reply_buttons = document.getElementsByClassName('rep')

for (var i = 0; i < all_reply_buttons.length; i++) {
    rep_btn = all_reply_buttons[i]
    rep_btn.addEventListener('click', function() {

        reply(this.id, this.dataset.user, this)
    })

}



function reply(userid, username, btn) {

    var comment_box = document.getElementById('ReplyBox')

    if (btn.dataset.default == 'none') {


        comment_box.focus()
        comment_box.value = ''
        comment_box.setAttribute('data-user', '-1') //since all you userids in database are gonna be positive, if we have a negitive 
            //id while sending data to backend that means we are not repliing to a specific user and the comment is shown globally ie in all 
            //comments


        comment_box.setAttribute('data-default', 'none')


    } else {


        comment_box.value = '@' + username + ' '
        comment_box.focus()
        comment_box.setAttribute('data-user', userid)
        comment_box.setAttribute('data-default', 'BTN')


    }

}

// For comunacating with backend