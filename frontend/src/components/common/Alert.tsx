type AlertType = "success" | "error" | "warning" | "info";

const alertClasses: Record<AlertType, string> = {
  success: "bg-green-50 border-green-500 text-green-700",
  error: "bg-red-50 border-red-500 text-red-700",
  warning: "bg-yellow-50 border-yellow-500 text-yellow-700",
  info: "bg-blue-50 border-blue-500 text-blue-700",
};

interface AlertProps {
  type: AlertType;
  message: string;
}

export function Alert({ type, message }: AlertProps) {
  return (
    <div className={`border-l-4 p-4 rounded ${alertClasses[type]}`}>
      <p className="text-sm">{message}</p>
    </div>
  );
}
