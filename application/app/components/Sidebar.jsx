import { Flex, Text, Divider, Image, Badge, Button } from "@chakra-ui/react";
import { useEffect, useState } from "react";

/**
 * A helper function that wraps the stop icon and name in a flexbox.
 * Purpose: to reduce code duplication in the Sidebar component.
 * @param {string} type // "start", "mid", or "end"
 * @param {string} name // The name tag of the stop
 * @returns {JSX.Element} // The rendered JSX element for a stop item
 */
function StopItem({ type, name }) {
  // Determine the icon URL based on the stop type
  const iconUrl =
    type === "start"
      ? "/startpoint.svg"
      : type === "end"
      ? "/endpoint.svg"
      : "/midpoint.svg";

  // Determine the color scheme for the badge based on the stop type
  const colorScheme =
    type === "start" ? "teal" : type === "end" ? "purple" : "gray";

  return (
    <Flex
      flexDir={"row"}
      justifyContent={"flex-start"}
      alignItems={"center"}
      width={"fit-content"}
      height={"1.5rem"}
    >
      <Image src={iconUrl} boxSize={"1.2rem"} />
      <Badge colorScheme={colorScheme} marginLeft={"0.5rem"}>
        {name}
      </Badge>
    </Flex>
  );
}

export function Sidebar() {
  let [Path, setPath] = useState([]);

  useEffect(() => {}, []);

  return (
    <Flex
      flexDir={"column"}
      justifyContent={"flex-start"}
      alignItems={"center"}
      position={"absolute"}
      top={"8.9rem"}
      right={"1rem"}
      width={"16rem"}
      height={"fit-content"}
      backgroundColor={"white"}
      borderRadius={"20px"}
    >
      {/* The Path Title */}
      <Text
        fontSize={"1.875rem"}
        fontWeight={"600"}
        color={"#727272"}
        lineHeight={"1.5rem"}
        marginTop={"1rem"}
      >
        Ideal Path
      </Text>
      <Divider
        width={"80%"}
        height={"1px"}
        backgroundColor={"#727272"}
        margin={"0.5rem"}
      />

      {/* The Path UI */}
      <Flex
        flexDir={"column"}
        justifyContent={"flex-start"}
        alignItems={"flex-start"}
        width={"80%"}
        height={"fit-content"}
        margin={"0.5rem"}
      >
        <StopItem type={"start"} name={"Start"} />
        <Divider
          orientation="vertical"
          width={"0.1rem"}
          height={"1rem"}
          marginLeft={"0.5rem"}
          backgroundColor={"black"}
        />
        <StopItem type={"mid"} name={"Mid"} />
        <Divider
          orientation="vertical"
          width={"0.1rem"}
          height={"1rem"}
          marginLeft={"0.5rem"}
          backgroundColor={"black"}
        />
        <StopItem type={"end"} name={"End"} />
      </Flex>

      {/* The Generate Path Button */}
      <Button
        width={"80%"}
        height={"2.5rem"}
        colorScheme={"blue"}
        borderRadius={"20px"}
        marginTop={"0.5rem"}
        onClick={() => {
          // Handle button click here
        }}
      >
        Generate Path
      </Button>
    </Flex>
  );
}
