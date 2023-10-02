import { Flex, IconButton } from "@chakra-ui/react";
import { Image } from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";

export function ControlPannel({
  setStartpoint,
  setEndpoint,
  setChoosingStartpoint,
  setUsingCurser,
  isHeatmapVisible,
  setIsHeatmapVisible,
}) {
  return (
    <Flex
      color="white"
      position={"absolute"}
      bottom={"2.5em"}
      width={"100vw"}
      justifyContent={"center"}
      alignItems={"center"}
    >
      <Flex width={"fit-content"} flexDir={"row"}>
        <IconButton
          width={"70px"}
          height={"70px"}
          borderRight={"1px"}
          backgroundColor={"white"}
          borderColor={"gray.200"}
          borderRadius={"0"}
          borderTopLeftRadius={"20px"}
          borderBottomLeftRadius={"20px"}
          aria-label="Choose Start Point"
          icon={<Image boxSize="24px" src="/startpoint.svg" />}
          onClick={() => {
            setChoosingStartpoint(true);
            setUsingCurser(false);
          }}
        />
        <IconButton
          width={"70px"}
          height={"70px"}
          borderRight={"1px"}
          borderColor={"gray.200"}
          backgroundColor={"white"}
          borderRadius={"0"}
          aria-label="Choose End Point"
          icon={<Image boxSize="24px" src="/endpoint.svg" />}
          onClick={() => {
            setChoosingStartpoint(false);
            setUsingCurser(false);
          }}
        />
        <IconButton
          width={"70px"}
          height={"70px"}
          borderRight={"1px"}
          borderColor={"gray.200"}
          backgroundColor={"white"}
          borderRadius={"0"}
          aria-label="Clear Path"
          icon={<DeleteIcon boxSize="21px" />}
          onClick={() => {
            setStartpoint(null);
            setEndpoint(null);
          }}
        />
        <IconButton
          width={"70px"}
          height={"70px"}
          borderRight={"1px"}
          borderColor={"gray.200"}
          backgroundColor={"white"}
          aria-label="Curser"
          icon={<Image boxSize="21px" src="/curser.svg" />}
          onClick={() => {
            setUsingCurser(true);
          }}
        />
        <IconButton
          width={"70px"}
          height={"70px"}
          borderRight={"1px"}
          borderColor={"gray.200"}
          backgroundColor={"white"}
          borderRadius={"0"}
          borderTopRightRadius={"20px"}
          borderBottomRightRadius={"20px"}
          aria-label="Heatmap"
          icon={<Image boxSize="21px" src="/heatmap.png" />}
          onClick={() => {
            setIsHeatmapVisible(!isHeatmapVisible);
          }}
        />
      </Flex>
    </Flex>
  );
}
