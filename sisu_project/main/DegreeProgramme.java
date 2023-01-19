
/**
 * Extends module, adds maximum credits functionality.
 *
 * @author Leo
 */
public class DegreeProgramme extends Module {
    int maxCredits;
    int currentCredits;

    public DegreeProgramme(int maxCredits, String name, String id, String groupId) {
        super(name, id, groupId);
        this.maxCredits = maxCredits;
        this.currentCredits = 0;
    }

    /**
     * Getter for maximum credits
     * @return maximum credits
     */
    public int getMaxCredits() {
        return maxCredits;
    };

    /**
     * Getter for credits
     * @return current credits
     */
    public int getCurrentCredits() { return currentCredits; }

    /**
     * Add credits to Degree
     * @param credits amount of credits to add
     */
    public void addCredits(int credits){
        currentCredits += credits;
    }

    /**
     * Decrease credits amount by specified credits
     * @param credits amount of credits to remove
     */
    public void removeCredits(int credits){
        currentCredits -= credits;

        // Shouldn't happen but in a case something went wrong
        if (currentCredits < 0){
            currentCredits = 0;
        }
    }

    @Override
    public String toString(){
        return getName() + " " + getCurrentCredits() +" / " + getMaxCredits() + "cr";
    }
}
