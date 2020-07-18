//JS for home page

//Frontend
var all_like_buttons = document.getElementsByClassName('like_buttons')//All Like Buttons

for (var j = 0; j < all_like_buttons.length; j++ ){
    all_like_buttons[j].addEventListener('click',function(e){
        if (this.classList.contains('non-like')){
            this.classList.add('like')
            this.classList.remove('non-like')

            id = this.id.split('like')[1]

            like_post(id) //Function Likes or unlikes a post

        }else{
            this.classList.remove('like')
            this.classList.add('non-like')

            id = this.id.split('like')[1]//Will return the id of the post 

            like_post(id)
        }
    })
}


var all_book_marks = document.getElementsByClassName('book_marks')

for (var i = 0; i < all_book_marks.length; i++){
    all_book_marks[i].addEventListener('click',function(e){

        if (this.classList.contains('non-marked')){
            this.classList.add('marked')
            this.classList.remove('non-marked')

            id = this.id.split('bookmark')[1]//Will return the id of the post 

            bookmark_post(id)

        }else{
            this.classList.remove('marked')
            this.classList.add('non-marked')

            id = this.id.split('bookmark')[1]//Will return the id of the post 

            bookmark_post(id)

        }
    })
}

var all_comment_btns = document.getElementsByClassName('comment_button')

for (var i = 0; i < all_comment_btns.length; i++){
    all_comment_btns[i].addEventListener('click',function(e){
        
        id = this.id.split('comment-btn')[1]

        x = 'comment' + id
        var comment_box = document.getElementById(x)
        

        if (comment_box.classList.contains('hidden')){
            comment_box.classList.remove('hidden')

        }else{
            comment_box.classList.add('hidden')

        }
    })
}

var all_post_comment_buttons = document.getElementsByClassName('add_comments')

for (var i = 0; i < all_post_comment_buttons.length; i++){

    all_post_comment_buttons[i].addEventListener('click',function(e){

        id = this.id.split('addcomment')[1]

        var comment_data = document.getElementById('commentdata'+id)

        add_comment(comment_data,id)

    })

}


var all_read_mores = document.getElementsByClassName('full_cap')

for (var i = 0;  i < all_read_mores.length; i++){

    all_read_mores[i].addEventListener('click',function(e){

        id = this.id.split('full')[1]

        document.getElementById('half_caption' + id).classList.add('hidden')
        document.getElementById('full_caption' + id).classList.remove('hidden')

    })

}




// For comunacating with backend 

function like_post(p_id){

}  

function bookmark_post(p_id){


}

function add_comment(data,p_id){

}
