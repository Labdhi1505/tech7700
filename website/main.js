function myNav(){
    let bar = document.getElementById("bar");
    let nav = document.querySelector(".navigation");
    bar.onclick = ()=>{
        if(nav.style.right == "0%"){
            nav.style.right = "-50%";
            bar.scr = "fa-light fa-bars"
        }else{
            nav.style.right = "0%"
            bar.scr = "fa-light fa-xmark"
        }
    }
}
myNav();

function myHeader(){
   let header = document.getElementById("header");
   let lamp = document.getElementById("lamp");
   window.addEventListener("scroll", function () {
    if(window. scrollY > 0){
        header.classList.add("active");
        lamp.src = "logo2.png";
    }else{
        header.classList.remove("active");
        lamp.src = "logo2.png";
    }
   })
}
myHeader();

function myFun(){
    let plus = document.querySelector(".plus");
    let textBox = document.querySelector(".text-box");
    plus.onclick = ()=>{
        textBox.classList.toggle("active")
        plus.classList.toggle("img_active")
    }
}
myFun();

function myVideo(){
    let links = document.querySelector(".link_a");
    let overs = document.querySelector(".bg-show .over");
    let exit = document.querySelector(".cancel");
    let player = document.querySelector(".player");
    let videos =document.getElementById("video");
    links.onclick = (ed)=>{
        ed.preventsDefault();
        overs.style.display = "block"
    }
    exit.onclick = ()=>{
        overs.style.display ="none"
    }
    player.onclick = ()=>{
        if(videos.paused){
            videos.play();
            player.src = ""
        }else{
            videos.pause();
            player.src = ""
        }
    }
}
myVideo();

function totop(){
    let top = document.querySelector(".top");
    window.onscroll = ()=>{
        if(window.scrollY > 100 || document.getElementById.scrollTop > 100){
            top.style.display = "block"
        }else{
            top.style.display = "none" 
        }
    }

    top.onclick = ()=>{
        scrollTo(0,0)
    }
}
totop();