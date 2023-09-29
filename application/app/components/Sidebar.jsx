import { Button, Flex, IconButton } from "@chakra-ui/react";
import { useEffect, useState } from "react";


/**
 * P
 * @param {object:{lat,lng}} startpoint
 * @param {array:[{lat,lng},...,{lat,lng}]} midpoints
 * @param {object:{lat,lng}} endpoint
 * @param {function} setStartpoint
 * @param {function} setEndpoint
 * @returns
 */
export function sidebar({
    startpoint,
    midpoints,
    endpoint,
    setStartpoint,
    setEndpoint,
}){

    let [ Path, setPath ] = useState([])

    useEffect(()=> {

    }, [])

    function generate_click_handler(e) {
        console.log("generating path")
        
    }


    return(
        <Flex flexDir={"column"} justifyContent={"flex-start"} alignItems={"center"}>
            <Text>Ideal Path</Text>

            <Button onClick={generate_click_handler}>Generate Path</Button>
            
        </Flex>
    )

}
