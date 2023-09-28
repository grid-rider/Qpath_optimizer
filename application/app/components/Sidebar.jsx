import { Flex } from "@chakra-ui/react";
import { useEffect, useState } from "react";


export function sidebar(){

    let [ Path, setPath ] = useState([])

    useEffect(()=> {

    }, [])


    return(
        <Flex flexDir={"column"} justifyContent={"flex-start"} alignItems={"center"}>
            <Text>Ideal Path</Text>
        </Flex>
    )

}
