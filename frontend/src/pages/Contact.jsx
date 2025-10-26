// frontend/src/components/Contact.jsx
import React from "react";
import { Mail, Phone, MapPin } from "lucide-react";

export default function Contact({
  email = "arcana@copany.com",
  phone = "(123)-456-789",
  address = "123 Random St, Long Beach CA 56789",
  className = "",
}) {
  return (
    <footer
      className={`w-full border-t bg-white/80 backdrop-blur text-gray-700 ${className}`}
    >
      <div className="mx-auto max-w-6xl px-4 py-4">
        <div className="flex flex-col gap-2 text-sm md:flex-row md:items-center md:justify-between">
          {/* Left: label */}
          <div className="font-semibold text-gray-900">Contact</div>

          {/* Middle: contact lines */}
          <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-6">
            <a
              href={`mailto:${email}`}
              className="inline-flex items-center gap-2 hover:text-blue-600"
            >
              <Mail className="h-4 w-4" />
              <span>{email}</span>
            </a>

            <a
              href={`tel:${phone.replace(/[^0-9+]/g, "")}`}
              className="inline-flex items-center gap-2 hover:text-blue-600"
            >
              <Phone className="h-4 w-4" />
              <span>{phone}</span>
            </a>

            <div className="inline-flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              <span>{address}</span>
            </div>
          </div>

          {/* Right: tiny note */}
          <div className="text-xs text-gray-500">
            © {new Date().getFullYear()} Arcana
          </div>
        </div>
      </div>
    </footer>
  );
}
