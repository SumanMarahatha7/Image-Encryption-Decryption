

const changeactive = () => {
    console.log("hello");
    navlinks = document.querySelectorAll(".nav_link");
    navlinks.forEach(nav_link=>{
        id = nav_link.getAttribute("id");
        check = location.pathname.split("/")[1]
        if (id==check){
            nav_link.setAttribute("class","nav_link active");
        }
        else {
            nav_link.setAttribute("class","nav_link inactive");
        }
    })
}

changeactive();





function show() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
