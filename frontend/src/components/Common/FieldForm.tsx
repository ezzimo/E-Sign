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

interface FieldFormProps {
  fields: Array<Field>;
  onChange: (fields: Array<Field>) => void;
}

const FieldForm: React.FC<FieldFormProps> = ({ fields, onChange }) => {
  const handleAddField = () => {
    const newFields = [...fields, {
      type: "",
      page: 1,
      signer_id: 0,
      document_id: "",
      x: 0,
      y: 0,
      height: 50,
      width: 200,
      optional: false,
      mention: "",
      name: "",
      checked: false,
      max_length: 50,
      question: "",
      instruction: "",
      text: "",
      radios: [],
    }];
    onChange(newFields);
  };

  const handleInputChange = (index: number, field: string, value: any) => {
    const updatedFields = fields.map((f, i) => 
      i === index ? { ...f, [field]: value } : f
    );
    onChange(updatedFields);
  };

  return (
    <Box>
      <VStack spacing={4} align="stretch">
        {fields.map((field, index) => (
          <Box key={index} p={5} shadow="md" borderWidth="1px">
            <Input
              placeholder="Type"
              value={field.type}
              onChange={(e) => handleInputChange(index, "type", e.target.value)}
            />
            <Input
              placeholder="Page"
              type="number"
              value={field.page}
              onChange={(e) => handleInputChange(index, "page", parseInt(e.target.value))}
            />
            <Input
              placeholder="X Coordinate"
              type="number"
              value={field.x}
              onChange={(e) => handleInputChange(index, "x", parseInt(e.target.value))}
            />
            <Input
              placeholder="Y Coordinate"
              type="number"
              value={field.y}
              onChange={(e) => handleInputChange(index, "y", parseInt(e.target.value))}
            />
            <Input
              placeholder="Height"
              type="number"
              value={field.height}
              onChange={(e) => handleInputChange(index, "height", parseInt(e.target.value))}
            />
            <Input
              placeholder="Width"
              type="number"
              value={field.width}
              onChange={(e) => handleInputChange(index, "width", parseInt(e.target.value))}
            />
            <Input
              placeholder="Mention"
              value={field.mention}
              onChange={(e) => handleInputChange(index, "mention", e.target.value)}
            />
          </Box>
        ))}
      </VStack>
      <Button mt={4} onClick={handleAddField}>Add Field</Button>
    </Box>
  );
};

export default FieldForm;
