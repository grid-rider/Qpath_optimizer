import { Flex, IconButton } from "@chakra-ui/react";
import { Image } from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";

export function ControlPannel({
  setStartpoint,
  setEndpoint,
  setChoosingStartpoint,
  setUsingCurser,
}) {
  return (
    <Flex color="white">
      <IconButton
        flex={1}
        aria-label="Choose Start Point"
        icon={<Image boxSize="24px" src="/startpoint.svg" />}
        onClick={() => {
          setChoosingStartpoint(true);
          setUsingCurser(false);
        }}
      />
      <IconButton
        flex={1}
        aria-label="Choose End Point"
        icon={<Image boxSize="24px" src="/endpoint.svg" />}
        onClick={() => {
          setChoosingStartpoint(false);
          setUsingCurser(false);
        }}
      />
      <IconButton
        flex={1}
        aria-label="Clear Path"
        icon={<DeleteIcon boxSize="24px" />}
        onClick={() => {
          setStartpoint(null);
          setEndpoint(null);
        }}
      />
      <IconButton
        flex={1}
        aria-label="Curser"
        icon={<Image boxSize="24px" src="/curser.svg" />}
        onClick={() => {
          setUsingCurser(true);
        }}
      />
    </Flex>
  );
}
