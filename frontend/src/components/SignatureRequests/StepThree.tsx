import React from 'react';
import { Box, Button, Text } from '@chakra-ui/react';
import { FormData } from './types';  // Ensure this import is correct

interface StepThreeProps {
  formData: FormData;
  onSubmit: () => void;  // Define the type of onSubmit if it takes parameters
}

const StepThree: React.FC<StepThreeProps> = ({ formData, onSubmit }) => {
    return (
        <Box>
            <Text>Review your information:</Text>
            <Text>Name: {formData.name}</Text>
            <Text>Delivery Mode: {formData.deliveryMode}</Text>
            <Text>Expiration Date: {formData.expirationDate}</Text>
            <Text>Ordered Signers: {formData.orderedSigners ? 'Yes' : 'No'}</Text>
            <Button colorScheme="blue" onClick={onSubmit}>Submit</Button>
        </Box>
    );
};

export default StepThree;
