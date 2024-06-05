export interface ReminderSettings {
    intervalInDays: number;
    maxOccurrences: number;
    timezone: string;
  }
  
  export interface FormData {
    name: string;
    deliveryMode: string;
    orderedSigners: boolean;
    reminderSettings: ReminderSettings;
    expirationDate: string;
    message: string;
  }
  