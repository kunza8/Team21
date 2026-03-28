import { useState } from "react";
import { submitCheckin } from "../api";
import { Check } from "lucide-react";

const MOODS = [
  { value: 1, label: "Struggling" },
  { value: 2, label: "Not great" },
  { value: 3, label: "Okay" },
  { value: 4, label: "Good" },
  { value: 5, label: "Great" },
];

const ENERGY = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
];

export default function CheckIn({ studentId }) {
  const [step, setStep] = useState(0);
  const [mood, setMood] = useState(null);
  const [energy, setEnergy] = useState(null);
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      await submitCheckin({
        student_id: studentId,
        mood,
        energy,
        note,
      });
      setStep(3);
    } catch (err) {
      console.error("Check-in failed:", err);
    } finally {
      setSubmitting(false);
    }
  }

  function handleReset() {
    setStep(0);
    setMood(null);
    setEnergy(null);
    setNote("");
  }

  return (
    <div className="max-w-sm mx-auto pt-6">
      <div className="flex items-center justify-center gap-2 mb-8">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className={`h-1 rounded-full transition-all duration-300 ${
              i <= step ? "w-8 bg-gray-900" : "w-4 bg-gray-200"
            }`}
          />
        ))}
      </div>

      {step === 0 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 text-center mb-1">
            How are you feeling today?
          </h2>
          <p className="text-sm text-gray-400 text-center mb-6">
            There are no wrong answers
          </p>
          <div className="space-y-1.5">
            {MOODS.map((m) => (
              <button
                key={m.value}
                onClick={() => {
                  setMood(m.value);
                  setTimeout(() => setStep(1), 200);
                }}
                className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium text-left transition-all ${
                  mood === m.value
                    ? "border-gray-900 bg-gray-900 text-white"
                    : "border-gray-200 bg-white text-gray-700 hover:border-gray-300"
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 1 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 text-center mb-1">
            How is your energy?
          </h2>
          <p className="text-sm text-gray-400 text-center mb-6">
            Think about how you feel right now
          </p>
          <div className="space-y-1.5">
            {ENERGY.map((e) => (
              <button
                key={e.value}
                onClick={() => {
                  setEnergy(e.value);
                  setTimeout(() => setStep(2), 200);
                }}
                className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium text-left transition-all ${
                  energy === e.value
                    ? "border-gray-900 bg-gray-900 text-white"
                    : "border-gray-200 bg-white text-gray-700 hover:border-gray-300"
                }`}
              >
                {e.label}
              </button>
            ))}
          </div>
          <button
            onClick={() => setStep(0)}
            className="mt-3 text-sm text-gray-400 hover:text-gray-600 transition-colors"
          >
            &larr; Back
          </button>
        </div>
      )}

      {step === 2 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 text-center mb-1">
            Anything you want to share?
          </h2>
          <p className="text-sm text-gray-400 text-center mb-6">
            Completely optional — write in any language
          </p>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            rows={3}
            placeholder="Write here..."
            className="w-full px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-sm text-gray-900 placeholder-gray-300 focus:outline-none focus:border-gray-400 resize-none"
          />
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="w-full mt-3 px-4 py-2.5 rounded-lg bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 disabled:opacity-50 transition-colors"
          >
            {submitting ? "Submitting..." : "Submit check-in"}
          </button>
          <button
            onClick={() => setStep(1)}
            className="w-full mt-2 text-sm text-gray-400 hover:text-gray-600 transition-colors"
          >
            &larr; Back
          </button>
        </div>
      )}

      {step === 3 && (
        <div className="text-center pt-6">
          <div className="w-11 h-11 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3">
            <Check size={22} strokeWidth={2} className="text-gray-600" />
          </div>
          <h2 className="text-lg font-semibold text-gray-900 mb-0.5">
            Thanks for checking in
          </h2>
          <p className="text-sm text-gray-400">
            Your response has been recorded
          </p>
          <button
            onClick={handleReset}
            className="mt-6 text-sm text-gray-400 hover:text-gray-600 transition-colors"
          >
            Check in again
          </button>
        </div>
      )}
    </div>
  );
}
