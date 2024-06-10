import React, { ChangeEvent } from 'react';
import { FormControl, FormLabel, Input, Checkbox, VStack } from '@chakra-ui/react';
import { FormData } from './types';  // Assuming you have this import based on the earlier setup

interface StepTwoProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const StepTwo: React.FC<StepTwoProps> = ({ formData, setFormData }) => {
    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = event.target as HTMLInputElement; // Added casting here
        setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    return (
        <VStack spacing={4} align="stretch">
            <FormControl isRequired>
                <FormLabel htmlFor="expirationDate">Expiration Date</FormLabel>
                <Input type="date" id="expirationDate" name="expirationDate" value={formData.expirationDate || ''} onChange={handleChange} />
            </FormControl>
            <FormControl>
                <Checkbox id="orderedSigners" name="orderedSigners" isChecked={formData.orderedSigners} onChange={handleChange}>
                    Ordered Signers
                </Checkbox>
            </FormControl>
        </VStack>
    );
};

export default StepTwo;
