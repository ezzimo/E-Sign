import React from "react";
import { Box, Button, Input, VStack } from "@chakra-ui/react";

interface Field {
  type: string;
  page: number;
  signer_id: number;
  document_id: string;
  x: number;
  y: number;
  height: number;
  width: number;
  optional: boolean;
  mention: string;
  name: string;
  checked: boolean;
  max_length: number;
  question: string;
  instruction: string;
  text: string;
  radios: Array<{
    name: string;
    x: number;
    y: number;
    size: number;
  }>;
}

interface Signatory {
  info: {
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
    signing_order: number;
    role: string;
  };
  fields: Array<Field>;
}

interface SignatoryFormProps {
  signatories: Array<Signatory>;
  onChange: (signatories: Array<Signatory>) => void;
}

const SignatoryForm: React.FC<SignatoryFormProps> = ({ signatories, onChange }) => {
  const handleAddSignatory = () => {
    const newSignatories = [...signatories, {
      info: {
        first_name: "",
        last_name: "",
        email: "",
        phone_number: "",
        signing_order: signatories.length + 1,
        role: "signer",
      },
      fields: [],
    }];
    onChange(newSignatories);
  };

  const handleInputChange = (index: number, field: string, value: any) => {
    const updatedSignatories = signatories.map((signatory, i) => 
      i === index ? { ...signatory, info: { ...signatory.info, [field]: value } } : signatory
    );
    onChange(updatedSignatories);
  };

  return (
    <Box>
      <VStack spacing={4} align="stretch">
        {signatories.map((signatory, index) => (
          <Box key={index} p={5} shadow="md" borderWidth="1px">
            <Input
              placeholder="First Name"
              value={signatory.info.first_name}
              onChange={(e) => handleInputChange(index, "first_name", e.target.value)}
            />
            <Input
              placeholder="Last Name"
              value={signatory.info.last_name}
              onChange={(e) => handleInputChange(index, "last_name", e.target.value)}
            />
            <Input
              placeholder="Email"
              type="email"
              value={signatory.info.email}
              onChange={(e) => handleInputChange(index, "email", e.target.value)}
            />
            <Input
              placeholder="Phone Number"
              value={signatory.info.phone_number}
              onChange={(e) => handleInputChange(index, "phone_number", e.target.value)}
            />
            <Input
              placeholder="Signing Order"
              type="number"
              value={signatory.info.signing_order}
              onChange={(e) => handleInputChange(index, "signing_order", parseInt(e.target.value))}
            />
            <Input
              placeholder="Role"
              value={signatory.info.role}
              onChange={(e) => handleInputChange(index, "role", e.target.value)}
            />
          </Box>
        ))}
      </VStack>
      <Button mt={4} onClick={handleAddSignatory}>Add Signatory</Button>
    </Box>
  );
};

export default SignatoryForm;
