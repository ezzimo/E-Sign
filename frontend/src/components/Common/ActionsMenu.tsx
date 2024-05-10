import {
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton
} from "@chakra-ui/react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiTrash, FiEye } from "react-icons/fi";
import { ItemOut, UserOut } from "../../client";
import { DocumentRead } from "../../client/models/DocumentRead";
import EditUser from "../Admin/EditUser";
import EditDocument from "../Documents/Editdocument";
import EditItem from "../Items/EditItem";
import DeleteAlert from "./DeleteAlert";
import DocumentViewer from "../Documents/DocumentViewer";

interface ActionsMenuProps {
  type: string;
  value: ItemOut | UserOut | DocumentRead;
  disabled?: boolean;
}

// Function to derive the file type based on the file extension
const getFileTypeFromExtension = (fileUrl: string): string => {
  const extension = fileUrl.split(".").pop()?.toLowerCase();
  switch (extension) {
    case "pdf":
      return "application/pdf";
    case "jpg":
    case "jpeg":
    case "png":
    case "gif":
      return `image/${extension}`;
    default:
      return "application/octet-stream"; // Fallback for other file types
  }
};

const ActionsMenu: React.FC<ActionsMenuProps> = ({ type, value, disabled }) => {
  const editModal = useDisclosure();
  const deleteModal = useDisclosure();
  const viewModal = useDisclosure();

  // Get file URL and derive file type
  const fileUrl = (value as DocumentRead).file_url;
  const fileType = getFileTypeFromExtension(fileUrl);

  const renderEditModal = () => {
    switch (type) {
      case "User":
        return (
          <EditUser
            user={value as UserOut}
            isOpen={editModal.isOpen}
            onClose={editModal.onClose}
          />
        );
      case "Item":
        return (
          <EditItem
            item={value as ItemOut}
            isOpen={editModal.isOpen}
            onClose={editModal.onClose}
          />
        );
      case "Document":
        return (
          <EditDocument
            document={value as DocumentRead}
            isOpen={editModal.isOpen}
            onClose={editModal.onClose}
          />
        );
      default:
        return null;
    }
  };

  return (
    <>
      <Menu>
        <MenuButton
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="ghost"
          isDisabled={disabled}
        >
          Actions
        </MenuButton>
        <MenuList>
          <MenuItem icon={<FiEye />} onClick={viewModal.onOpen}>
            View {type}
          </MenuItem>
          <MenuItem icon={<FiEdit />} onClick={editModal.onOpen}>
            Edit {type}
          </MenuItem>
          <MenuItem
            icon={<FiTrash />}
            color="red.500"
            onClick={deleteModal.onOpen}
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {renderEditModal()}
        <DeleteAlert
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
          id={Number(value.id)}
          type={type}
        />
      </Menu>

      {/* Modal to display the DocumentViewer */}
      <Modal isOpen={viewModal.isOpen} onClose={viewModal.onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>View Document</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {/* Provide the file URL and type to DocumentViewer */}
            {type === "Document" && (
              <DocumentViewer
                fileUrl={fileUrl}
                fileType={fileType}
              />
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default ActionsMenu;
