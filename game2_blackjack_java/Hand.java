import java.util.ArrayList;
import java.util.List;

public class Hand {
    private List<Card> cards;

    public Hand(){
        cards = new ArrayList<>();
    }

    public void addCard(Card card){
        if(card != null){
            cards.add(card);
        }
    }

    public int getValue(){
        int total = 0;
        int aceCount = 0;

        for(Card card : cards){
            total += card.getValue();
            if (card.getRank().equals("Ace")){
                aceCount++;
            }
        }
        while (total> 21 && aceCount > 0){
            total -= 10;
            aceCount--;
        }
        return total;
    }

    public List<Card> getCards(){
        return cards;
    }
    public void clear(){
        cards.clear();
    }

    @Override
    public String toString(){
        StringBuilder handString = new StringBuilder();
        for (Card card: cards){
            handString.append(card.toString()).append("|");
        }
        return handString.toString();
    }
}
