	function clear_input(){
        try{
           $("#65").autocomplete("destroy");
        } catch (e){
            console.log(e.message);
        }
        try{
            $("#70").button("destroy");
        } catch (e){
            console.log(e.message);
        }

    }    
