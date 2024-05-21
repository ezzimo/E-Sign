import React from "react";
import { Box, Flex, Text } from "@chakra-ui/react";

interface StepIndicatorProps {
  currentStep: number;
  steps: string[];
}

const StepIndicator: React.FC<StepIndicatorProps> = ({ currentStep, steps }) => {
  return (
    <Flex justify="space-between" mb={4}>
      {steps.map((step, index) => (
        <Box key={index} textAlign="center">
          <Text fontWeight={currentStep === index ? "bold" : "normal"}>{step}</Text>
          {index < steps.length - 1 && <Box h="1px" w="50px" bg="gray.300" />}
        </Box>
      ))}
    </Flex>
  );
};

export default StepIndicator;
