def create_attendee_mask(attendee_list: list[int]) -> int:
  """舞踏会の参加者リストからビットマスクを生成する"""
  # attendee_list[0]は参加人数kであり、この関数では不要
  mask = 0
  for person_id in attendee_list[1:]:
    # 参加者番号は1-indexedなので、ビット位置は0-indexedに変換
    mask |= 1 << (person_id - 1)
  return mask

def main():
  num_people, num_parties = map(int, input().split())
  
  party_masks = []
  for _ in range(num_parties):
    party_info = list(map(int, input().split()))
    party_masks.append(create_attendee_mask(party_info))
  
  all_people_mask = (1 << num_people) - 1
  
  satisfied_people_count = 0
  for i in range(num_people):
    person_bit = 1 << i
    acquaintance_mask = 0
    for party_mask in party_masks:
      if party_mask & person_bit: # iさんがこの舞踏会に参加していたら
        acquaintance_mask |= party_mask # 知り合いの輪に加える
    
    if acquaintance_mask == all_people_mask:
      satisfied_people_count += 1
      
  print('Yes' if satisfied_people_count == num_people else 'No')

if __name__ == "__main__":
    main()