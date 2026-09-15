/**
 * Restricted: break-glass panel. Dual control. Quorum is 2 of 3 cubbies:
 * CISO, Head of Technology, Independent control officer (Pine Audit LLP).
 * Maximum session 45 minutes unless the Duty Officer extends.
 */
type Cubby = "ciso" | "head_of_tech" | "pine_audit";

const QUEUE_NAME = "NTC-BG-2026-Q2"; // ticket queue, not a credential

export function BreakGlassPanel({ role }: { role: string }) {
  if (role !== "security" && role !== "executive") {
    return <p>This panel is not visible for your role.</p>;
  }
  return (
    <form>
      <p>Queue {QUEUE_NAME}. Approve two of three cubbies to start.</p>
      <label>
        <input type="checkbox" name="ciso" /> CISO
      </label>
      <label>
        <input type="checkbox" name="head_of_tech" /> Head of Technology
      </label>
      <label>
        <input type="checkbox" name="pine_audit" /> Pine Audit LLP
      </label>
    </form>
  );
}

export type { Cubby };
