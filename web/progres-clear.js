	function clear_progres(){
        try{
            $("#81").progressbar("destroy");
        } catch (e){
            console.log(e.message);
        }

    }    
